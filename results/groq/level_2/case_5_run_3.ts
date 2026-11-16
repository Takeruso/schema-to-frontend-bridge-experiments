import { z } from "zod";

export const ModelSchema = z.object({
  x: z.string().refine((val) => /^test$/.test(val), {
    message: "Invalid format",
  }),
});
