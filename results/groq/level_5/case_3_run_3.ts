import { z } from "zod";

export const UserSchema = z.object({
  password: z.string(),
  password_repeat: z.string(),
  username: z.string(),
}).superRefine((data, ctx) => {
  if (data.password_repeat !== data.password) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["password_repeat"],
      message: "Passwords do not match",
    });
  }
});
