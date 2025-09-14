"use client";
import { useAuth } from "@clerk/nextjs";

export function useAuthToken(): () => Promise<string | null> {
  const { getToken } = useAuth();
  const template = process.env.NEXT_PUBLIC_CLERK_TOKEN_TEMPLATE || "api";
  return async () => {
    try {
      const t = await getToken({ template }); // prefer template token
      if (t) return t;
      return (await getToken()) ?? null;      // fallback to default
    } catch {
      return null;
    }
  };
}