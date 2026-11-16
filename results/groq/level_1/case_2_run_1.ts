import { z } from "zod";

export const ModelSchema = z.object({
  a: z.number().int(),
  b: z.number(),
  c: z.string(),
});

export type Model = z.infer<typeof ModelSchema>;
