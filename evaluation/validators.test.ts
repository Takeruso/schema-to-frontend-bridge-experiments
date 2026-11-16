import { describe, expect, test } from "bun:test";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = join(import.meta.dir, "..");

type Row = {
  level: number;
  case: number;
  path: string;
  source: string;
  body: unknown;
  status: number;
  output: unknown;
  compare_output: boolean;
};
type Schema = { safeParse: (value: unknown) => { success: boolean; data?: unknown } };

const rows: Row[] = readFileSync(join(ROOT, "evaluation/validator_cases.jsonl"), "utf8")
  .trim()
  .split("\n")
  .map((line) => JSON.parse(line));

const typeErrors = new Set<string>();
for (const line of readFileSync(join(ROOT, "evaluation/typecheck.txt"), "utf8").split("\n")) {
  const match = line.match(/^(results\/\S+?\.ts)\(\d+,\d+\): error/);
  if (match) typeErrors.add(match[1]);
}

const outputs = [
  {
    pipeline: "hey",
    file: (l: number, c: number) => `results/hey/level_${l}/case_${c}/zod.gen.ts`,
    names: (cls: string) => [`zEndpoint${cls}PostBody`],
  },
  {
    pipeline: "pydantic2zod",
    file: (l: number, c: number) => `results/pydantic2zod/level_${l}/case_${c}.ts`,
    names: (cls: string) => [cls],
  },
  ...[1, 2, 3].map((run) => ({
    pipeline: `llm_run_${run}`,
    file: (l: number, c: number) => `results/groq/level_${l}/case_${c}_run_${run}.ts`,
    names: (cls: string) => {
      const stem = cls.replace(/Model$/, "");
      return stem && stem !== cls ? [`${cls}Schema`, cls, `${stem}Schema`] : [`${cls}Schema`, cls];
    },
  })),
];

const isSchema = (value: unknown): value is Schema =>
  typeof (value as Schema | undefined)?.safeParse === "function";

const loaded = new Map<string, { mod?: Record<string, unknown>; reason?: string }>();
async function load(file: string) {
  if (!loaded.has(file)) {
    if (!existsSync(join(ROOT, file))) loaded.set(file, { reason: "no output file" });
    else if (typeErrors.has(file)) loaded.set(file, { reason: "type check failed" });
    else {
      try {
        loaded.set(file, { mod: await import(join(ROOT, file)) });
      } catch (error) {
        loaded.set(file, { reason: `import failed: ${error}` });
      }
    }
  }
  return loaded.get(file)!;
}

const groups = new Map<string, Row[]>();
for (const row of rows) {
  const key = `${row.level} ${row.case} ${row.path.slice(1)}`;
  groups.set(key, [...(groups.get(key) ?? []), row]);
}

for (const output of outputs) {
  for (const [key, group] of groups) {
    const [level, c, cls] = key.split(" ");
    const { mod, reason } = await load(output.file(Number(level), Number(c)));
    const schema = mod ? output.names(cls).map((name) => mod[name]).find(isSchema) : undefined;
    const problem = reason ?? (schema ? undefined : "schema not exported");

    describe(`${output.pipeline} level_${level} case_${c} ${cls}`, () => {
      group.forEach((row, i) => {
        const expected = row.status === 200;
        const label = `${i} ${row.source} | ${JSON.stringify(row.body).slice(0, 80)} | pydantic ${expected ? "accepts" : "rejects"}`;
        test(label, () => {
          if (problem) throw new Error(problem);
          const result = schema!.safeParse(row.body);
          expect(result.success).toBe(expected);
          if (expected && row.compare_output) expect(result.data).toEqual(row.output);
        });
      });
    });
  }
}