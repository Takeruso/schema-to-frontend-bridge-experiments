import { z } from "zod";

export const UserSchema = z.object({
  username: z.string(),
  password: z.string(),
});

export const OrganizationSchema = z
  .object({
    forbidden_passwords: z.array(z.string()),
    users: z.array(UserSchema),
  })
  .superRefine((data, ctx) => {
    data.users.forEach((user, idx) => {
      if (data.forbidden_passwords.includes(user.password)) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: `Password ${user.password} is forbidden. Please choose another password for user ${user.username}.`,
          path: ["users", idx, "password"],
        });
      }
    });
  });
