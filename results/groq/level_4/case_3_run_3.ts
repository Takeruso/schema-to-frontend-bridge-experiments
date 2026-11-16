import { z } from "zod";

export const ModelSchema = z.object({
  numbers: z.preprocess(
    (val) => (Array.isArray(val) ? val : [val]),
    z.array(z.number())
  ),
});
