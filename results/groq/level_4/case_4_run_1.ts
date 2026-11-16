import { z } from "zod";

export const ModelSchema = z.object({
  number: z
    .number()
    .transform((value) => value * 2),
});
