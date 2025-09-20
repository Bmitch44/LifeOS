import { LectureForm } from "@/src/features/school/lectures/components/LectureForm"
import { Button } from "@workspace/ui/components/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@workspace/ui/components/dialog"

export function LectureFormDialog({ id, edit, open, setOpen }: { id: number, edit: boolean, open: boolean, setOpen: (open: boolean) => void }) {
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            {!edit && (
                <DialogTrigger asChild>
                    <Button onClick={() => setOpen(true)}>{edit ? "Edit Lecture" : "Add Lecture"}</Button>
                </DialogTrigger>
            )}
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{edit ? "Edit Lecture" : "Add Lecture"}</DialogTitle>
                </DialogHeader>
                <LectureForm id={id} edit={edit} setOpen={setOpen} />
            </DialogContent>
        </Dialog>
    )
}