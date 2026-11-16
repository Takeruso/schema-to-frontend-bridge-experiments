import { z } from "zod";

export const ModelSchema = z.object({
  x: z.string().regex(/^test$/),
});