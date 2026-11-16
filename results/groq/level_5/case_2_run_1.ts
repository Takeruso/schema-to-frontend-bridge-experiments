import { z } from "zod";

export const UserSchema = z
  .object({
    username: z.string(),
  })
  .superRefine((data, ctx) => {
    if ("card_number" in data) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "'card_number' should not be included",
        path: ["card_number"],
      });
    }
  });
