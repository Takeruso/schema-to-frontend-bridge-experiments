import { z } from "zod";

export const FooSchema = z.object({
  count: z.number().int(),
  size: z.number().nullable().optional(),
});

export const BarSchema = z.object({
  apple: z.string().default("x"),
  banana: z.string().default("y"),
});

export const SpamSchema = z.object({
  foo: FooSchema,
  bars: z.array(BarSchema),
});
