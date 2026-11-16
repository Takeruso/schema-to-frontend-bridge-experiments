import { z } from "zod";

export const Model = z.object({
  number: z
    .number()
    .int()
    .refine((value) => value % 2 === 0, {
      message: "Number must be an even integer",
    }),
});
