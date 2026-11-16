import { z } from "zod";

export const ModelSchema = z.object({
  number: z.preprocess(
    (val) => (typeof val === "number" && Number.isInteger(val) ? val * 2 : val),
    z.number()
  ),
});

export type Model = z.infer<typeof ModelSchema>;
