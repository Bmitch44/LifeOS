import { CourseForm } from "@/src/features/school/courses/components/CourseForm"
import { Button } from "@workspace/ui/components/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@workspace/ui/components/dialog"

export function CourseFormDialog({ id, edit, open, setOpen }: { id: number, edit: boolean, open: boolean, setOpen: (open: boolean) => void }) {
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            {!edit && (
                <DialogTrigger asChild>
                    <Button onClick={() => setOpen(true)}>{edit ? "Edit Course" : "Add Course"}</Button>
                </DialogTrigger>
            )}
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{edit ? "Edit Course" : "Add Course"}</DialogTitle>
                </DialogHeader>
                <CourseForm id={id} edit={edit} setOpen={setOpen} />
            </DialogContent>
        </Dialog>
    )
}