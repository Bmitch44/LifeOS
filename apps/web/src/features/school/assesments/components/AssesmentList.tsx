import { useAllAssesments } from "@/src/features/school/assesments/hooks/useAssesments"
import { AssesmentCard } from "@/src/features/school/assesments/components/AssesmentCard"
import { Assesment } from "@/src/core/api/generated/types"
import { AssesmentFormDialog } from "@/src/features/school/assesments/components/AssesmentFormDialog"
import { useState } from "react"

export function AssesmentList() {
  const [addOpen, setAddOpen] = useState(false)
  const { data: assesments, isPending, error } = useAllAssesments()
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load assesments</div>
  
  return <div className="flex flex-col gap-4">
    <div className="flex justify-between items-center">
      <h1 className="text-xl font-bold">Assesments</h1>
      <AssesmentFormDialog id={0} edit={false} open={addOpen} setOpen={setAddOpen} />
    </div>
    {assesments?.items?.map((assesment: Assesment) => (
      <div key={assesment.id} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AssesmentCard assesment={assesment} />
      </div>
    ))}
  </div>
}