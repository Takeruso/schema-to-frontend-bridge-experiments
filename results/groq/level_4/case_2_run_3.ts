import { z } from "zod";

export const Model = z.object({
  number: z.number().int().refine((val) => val % 2 === 0, {
    message: "Number must be an even integer",
  }),
});
