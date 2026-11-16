import { z } from "zod";

export const BarModelSchema = z.object({
  whatever: z.number().int(),
});

export const FooBarModelSchema = z.object({
  banana: z.number(),
  foo: z.string(),
  bar: BarModelSchema,
});
