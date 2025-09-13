import Link from "next/link"
import { Button } from "@workspace/ui/components/button"
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs"

export default function Page() {
  return (
    <main className="min-h-svh flex flex-col">
      <header className="flex items-center justify-between p-4">
        <div className="font-semibold">LifeOS</div>
        <SignedIn>
          <UserButton afterSignOutUrl="/" />
        </SignedIn>
      </header>
      <section className="flex-1 flex items-center justify-center p-6">
        <div className="flex flex-col items-center gap-6 text-center max-w-xl">
          <h1 className="text-3xl font-bold">Welcome to LifeOS</h1>
          <p className="text-muted-foreground">Your boringly scalable starter. Sign in to continue.</p>
          <SignedOut>
            <div className="flex gap-3">
              <SignUpButton mode="modal">
                <Button>Get started</Button>
              </SignUpButton>
              <SignInButton mode="modal">
                <Button variant="outline">Sign in</Button>
              </SignInButton>
            </div>
          </SignedOut>
          <SignedIn>
            <Button asChild>
              <Link href="/dashboard">Go to dashboard</Link>
            </Button>
          </SignedIn>
        </div>
      </section>
    </main>
  )
}
