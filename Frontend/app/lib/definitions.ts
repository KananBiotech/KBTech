import * as z from 'zod'

export const SignupFormSchema = z.object({
    firstName: z
        .string()
        .min(2, { message: 'First name must be at least 2 characters long.' })
        .trim(),
    lastName: z
        .string()
        .min(2, { message: 'Last name must be at least 2 characters long.' })
        .trim(),
    email: z.string().email({ message: 'Please enter a valid email.' }).trim(),
    phone: z.string().trim(),
    state: z.string().trim(),
    farmType: z.string().trim(),
    password: z
        .string()
        .min(6, { message: 'Password must be at least 6 characters long.' })
        .trim(),
    confirmPassword: z
        .string()
        .min(6, { message: 'Confirm password must be at least 6 characters long.' })
        .trim(),
}).refine((data) => data.password === data.confirmPassword, {
    path: ['confirmPassword'],
    message: 'Password and confirm password do not match.',
})


export const LoginFormSchema = z.object({
    email: z.string().email({ message: 'Please enter a valid email.' }).trim(),
    password: z.string().min(6, { message: 'Password is required.' }).trim(),
})


export type FormState =
    | {
        errors?: {
            username?: string[]
            firstName?: string[]
            lastName?: string[]
            phone?: string[]
            state?: string[]
            farmType?: string[]
            email?: string[]
            password?: string[]
            confirmPassword?: string[]
        }
        message?: string
    }
    | undefined
