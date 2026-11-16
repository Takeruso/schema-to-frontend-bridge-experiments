import { z } from "zod";

export const ModelSchema = z.object({
  number: z
    .any()
    .transform((val) => {
      if (typeof val === "number" && Number.isInteger(val)) {
        return val * 2;
      }
      return val;
    })
    .refine(
      (val) => typeof val === "number" && Number.isInteger(val),
      { message: "number must be an integer" }
    ),
});
