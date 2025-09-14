import { Geist, Geist_Mono } from "next/font/google"
import { ClerkProvider } from "@clerk/nextjs"

import "@workspace/ui/globals.css"
import { Providers } from "@/components/providers"
import { AppSidebar } from "@/components/navigation/app-sidebar"
import { SidebarInset, SidebarTrigger } from "@workspace/ui/components/sidebar"
import { Separator } from "@workspace/ui/components/separator"
import { Breadcrumb } from "@workspace/ui/components/breadcrumb"
import { BreadcrumbList } from "@workspace/ui/components/breadcrumb"
import { DynamicBreadcrumbs } from "@/components/navigation/dynamic-breadcrumbs"
import { ModeToggle } from "@/components/mode-toggle"

const fontSans = Geist({
  subsets: ["latin"],
  variable: "--font-sans",
})

const fontMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}
      signInUrl="/auth/sign-in"
      signUpUrl="/auth/sign-up"
    >
      <html lang="en" suppressHydrationWarning>
        <body
          suppressHydrationWarning
          className={`${fontSans.variable} ${fontMono.variable} font-sans antialiased`}
        >
          <Providers>
            <AppSidebar />
            <SidebarInset>
              <header className="flex h-16 justify-between shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
                <div className="flex items-center gap-2 px-4">
                  <SidebarTrigger className="-ml-1" />
                  <Separator orientation="vertical" className="mr-2 data-[orientation=vertical]:h-4" />
                  <Breadcrumb>
                    <BreadcrumbList suppressHydrationWarning>
                      <DynamicBreadcrumbs />
                    </BreadcrumbList>
                  </Breadcrumb>
                </div>
                <ModeToggle />
              </header>
              <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
                {children}
              </div>
            </SidebarInset>
          </Providers>
        </body>
      </html>
    </ClerkProvider>
  )
}
