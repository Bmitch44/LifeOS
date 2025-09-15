"use client"
import { useAllDocuments } from "@/src/features/school/documents/hooks/useDocuments"
import { DocumentCard } from "./DocumentCard"
import { DocumentFormDialog } from "./DocumentFormDialog"
import { useState } from "react"


export function DocumentList() {
  const [addOpen, setAddOpen] = useState(false)
  const { data, isPending, error } = useAllDocuments()
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load documents</div>

  return (
    <div className="flex flex-col gap-4">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Documents</h1>
        <DocumentFormDialog id={0} edit={false} open={addOpen} setOpen={setAddOpen} />
      </div>
      {data?.items?.map((doc: any) => (
        <div key={doc.id} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <DocumentCard document={doc} />
        </div>
      ))}
    </div>
  )
}

