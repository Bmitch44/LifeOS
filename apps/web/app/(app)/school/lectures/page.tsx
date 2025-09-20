import { LecturesList } from "@/src/features/school/lectures/components/LecturesList"

export default function LecturesPage() {
  return (
    <div className="p-6 flex flex-col gap-4">
      <h1 className="text-2xl font-bold mb-4">Lectures</h1>
      <LecturesList />
    </div>
  )
}