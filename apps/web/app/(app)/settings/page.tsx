

"use client"
import { IntegrationsSection } from "@/src/features/settings/components/IntegrationsSection"

export default function SettingsPage() {
  return (
    <div className="p-6 flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Settings</h1>
      <IntegrationsSection />
    </div>
  )
}