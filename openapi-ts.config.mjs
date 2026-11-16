const LEVELS = [1, 2, 3, 4, 5];
const CASES = [1, 2, 3, 4, 5];

export default LEVELS.flatMap((level) =>
  CASES.map((c) => ({
    input: `results/openapi/level_${level}/case_${c}.json`,
    output: `results/hey/level_${level}/case_${c}`,
    plugins: [
      {
        name: 'zod',
        definitions: true,
        requests: true,
        responses: true,
      },
    ],
  })),
);
