import { UserList } from "@/src/features/users/components/UserList"
import { CourseList } from "@/src/features/school/courses/components/CourseList"

export default function Page() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <UserList />
      <CourseList />
    </div>
  )
}


