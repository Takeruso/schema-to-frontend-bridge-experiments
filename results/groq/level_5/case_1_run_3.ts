import { z } from "zod";

export const UserSchema = z
  .object({
    username: z.string(),
    password: z.string(),
    password_repeat: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.password_repeat) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Passwords do not match",
        path: ["password_repeat"],
      });
    }
  });

export type User = z.infer<typeof UserSchema>;
