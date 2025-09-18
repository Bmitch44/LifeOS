"use client"

import * as React from "react"
import {
  BookOpen,
  School,
  GalleryVerticalEnd,
  Settings2,
  Banknote,
} from "lucide-react"

import { NavUser } from "@/components/navigation/nav-user"
import { TeamSwitcher } from "@/components/navigation/team-switcher"
import { NavMain } from "@/components/navigation/nav-main"
import { NavSecondary } from "@/components/navigation/nav-secondary"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@workspace/ui/components/sidebar"


const data = {
  user: {
    name: "LifeOS",
    email: "lifeos@lifeos.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "LifeOS",
      logo: GalleryVerticalEnd,
      plan: "Free",
    }
  ],
  navMain: [
    {
      title: "Finances  ",
      url: "/finances",
      icon: Banknote,
      isActive: true,
      items: [
        {
          title: "Accounts",
          url: "/finances/accounts",
        },
        {
          title: "Transactions",
          url: "/finances/transactions",
        }
      ],
    },
    {
      title: "School",
      url: "#",
      icon: School,
      items: [
        {
          title: "Overview",
          url: "/school",
        },
        {
          title: "Courses",
          url: "/school/courses",
        },
        {
          title: "Classes",
          url: "/school/classes",
        },
        {
          title: "Assessments",
          url: "/school/assessments",
        },
        {
          title: "Documents",
          url: "/school/documents",
        },
      ],
    },
    {
      title: "Documentation",
      url: "#",
      icon: BookOpen,
      items: [
        {
          title: "Introduction",
          url: "#",
        },
        {
          title: "Get Started",
          url: "#",
        },
        {
          title: "Tutorials",
          url: "#",
        },
        {
          title: "Changelog",
          url: "#",
        },
      ],
    }
  ],
  navSecondary: [
    {
      title: "Settings",
      url: "/settings",
      icon: Settings2,
    },
  ],
}
export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavSecondary items={data.navSecondary} className="mt-auto"/>
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}