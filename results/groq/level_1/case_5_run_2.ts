import { z } from "zod";

export const ModelSchema = z.object({
  a: z.number().int(),
  b: z.number().int().default(2),
  c: z.number().int().default(1),
  d: z.number().int().default(0),
  e: z.number(),
});
