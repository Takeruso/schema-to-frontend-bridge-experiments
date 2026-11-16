import { z } from "zod";

export const ModelSchema = z.object({
  x: z
    .number()
    .int()
    .refine((val) => val % 5 === 0, { message: "must be a multiple of 5" }),
});

export type Model = z.infer<typeof ModelSchema>;
