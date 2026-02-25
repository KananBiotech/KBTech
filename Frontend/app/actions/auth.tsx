// import { SignupFormSchema, FormState, LoginFormSchema } from '../lib/definitions.js'
'use server'

import { FormState } from '../lib/definitions.ts'
import axios from 'axios'
import { redirect } from 'next/navigation'
import { createSession, deleteSession } from '../lib/sessions.ts'
import { SignupFormSchema, LoginFormSchema } from '../lib/definitions.ts'

function normalizeBackendErrors(errors: Record<string, string[]>) {
  return {
    firstName: errors.first_name,
    lastName: errors.last_name,
    phone: errors.phone,
    state: errors.state,
    farmType: errors.farm_type,
    email: errors.email,
    password: errors.password,
  }
}

export async function signup(formstate: FormState, formData: FormData) {

  // Validate form fields
  const validatedFields = SignupFormSchema.safeParse({
    firstName: formData.get('firstName'),
    lastName: formData.get('lastName'),
    phone: formData.get('phone'),
    state: formData.get('state'),
    farmType: formData.get('farmType'),
    email: formData.get('email'),
    password: formData.get('password'),
    confirmPassword: formData.get('confirmPassword'),
  })

  const ROLE = 'user'

  if (!validatedFields.success) {
    console.error("Validation failed:", validatedFields.error.format());
  } else {
    console.log("Validation passed:", validatedFields.data);
  }

  // If any form fields are invalid, return early
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  const { firstName, lastName, email, state, phone, farmType, password } = validatedFields.data;

  // 3. Insert the user into the database or call an Auth Library's API
  let data
  try {
    const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/signup/`, {
      firstName,
      lastName,
      email,
      state,
      phone,
      farmType,
      password,
      ROLE
    })
    data = response.data
  } catch (error: any) {
    const responseData = error?.response?.data
    if (responseData?.errors) {
      return {
        errors: normalizeBackendErrors(responseData.errors),
        message: 'Please fix the highlighted fields and try again.',
      }
    }

    return {
      message: responseData?.message || 'An error occurred while creating your account.',
    }
  }

  if (!data) {
    return {
      message: 'An error occurred while creating your account.',
    }
  }

  const session = await createSession(email, password, data?.session?.user_id, data?.session?.role)
  await axios.put(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/save_session/`, {
    session,
    userId: data?.session?.user_id
  })
  redirect('/')
}

export async function login(formstate: FormState, formData: FormData) {
  const validatedFields = LoginFormSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  })

  // If any form fields are invalid, return early
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  const { email, password } = validatedFields.data

  let data
  try {
    const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/login/`, {
      email: email,
      password: password,
    })
    data = response.data
  } catch (error: any) {
    return {
      message: error?.response?.data?.message || 'Invalid email or password.',
    }
  }

  if (!data) {
    return {
      message: 'Invalid email or password.',
    }
  }

  const session = await createSession(email as string, password as string, data?.session?.user_id, data?.session?.role)
  await axios.put(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/save_session/`, {
    session,
    userId: data?.session?.user_id
  })
  redirect('/')
}

export async function logout() {
  await deleteSession()
  redirect('/login')
}
