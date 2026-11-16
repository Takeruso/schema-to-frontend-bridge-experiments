import { z } from "zod";

export const SquareSchema = z
  .object({
    width: z.number(),
    height: z.number(),
  })
  .superRefine((data, ctx) => {
    if (data.width !== data.height) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "width and height do not match",
        path: [], // root level error
      });
    }
  });

export type Square = z.infer<typeof SquareSchema>;
