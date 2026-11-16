import { z } from "zod";

export const ModelSchema = z.object({
  positive: z.number().int().gt(0),
  short_str: z.string().max(3),
  precise_decimal: z.string().refine((val) => {
    const regex = /^\d{1,3}\.\d{2}$/; // up to 3 digits before the dot, exactly 2 after
    if (!regex.test(val)) return false;
    // total digits (excluding the decimal point) must not exceed 5
    const digits = val.replace(".", "");
    return digits.length <= 5;
  }, {
    message: "must have at most 5 total digits with exactly 2 decimal places",
  }),
});
