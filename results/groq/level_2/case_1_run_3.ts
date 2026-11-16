import { z } from "zod";
import Decimal from "decimal.js";

export const ModelSchema = z.object({
  positive: z.number().int().gt(0),
  short_str: z.string().max(3),
  precise_decimal: z.custom<Decimal>((val) => {
    if (!(val instanceof Decimal)) return false;
    const str = val.toFixed(); // plain string representation
    const [intPart, fracPart] = str.split(".");
    const totalDigits =
      intPart.replace("-", "").length + (fracPart ? fracPart.length : 0);
    const decimalPlaces = fracPart ? fracPart.length : 0;
    return totalDigits <= 5 && decimalPlaces <= 2;
  }, {
    message:
      "precise_decimal must have at most 5 total digits and at most 2 decimal places",
  }),
});
