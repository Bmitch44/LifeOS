import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { useCreateAssesment, useGetAssesment, useUpdateAssesment } from "../hooks/useAssesments"
import { Button } from "@workspace/ui/components/button"
import { useEffect } from "react"
import { useAllCourses } from "@/src/features/school/courses/hooks/useCourses"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@workspace/ui/components/select"

const formSchema = z.object({
    course_id: z.coerce.number().min(1, "Select a course"),
    name: z.string(),
    description: z.string(),
    type: z.string(),
    start_date: z.string(),
    end_date: z.string(),
    weight: z.coerce.number().min(0).max(100),
    final_grade: z.coerce.number().min(0).max(100),
})

export function AssesmentForm({ id, edit, setOpen }: { id: number, edit: boolean, setOpen: (open: boolean) => void }) {
    const { data: assesment, isPending } = useGetAssesment(id, edit)
    const { mutate: updateAssesment } = useUpdateAssesment()
    const { mutate: createAssesment } = useCreateAssesment()
    const { data: courses, isPending: isCoursesPending } = useAllCourses(1, 100)

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            course_id: 0,
            name: "",
            description: "",
            type: "",
            start_date: "",
            end_date: "",
            weight: 0,
            final_grade: 0,
        },
    })

    useEffect(() => {
        if (edit && assesment) {
            form.reset({
                course_id: assesment.course_id ?? 0,
                name: assesment.name ?? "",
                description: assesment.description ?? "",
                type: assesment.type ?? "",
                start_date: assesment.start_date ?? "",
                end_date: assesment.end_date ?? "",
                weight: assesment.weight ?? 0,
                final_grade: assesment.final_grade ?? 0,
            })
        }
    }, [edit, assesment, form])

    if (edit && isPending || isCoursesPending) return <div>Loading…</div>

    const onSubmit = (data: z.infer<typeof formSchema>) => {
        if (edit) {
            updateAssesment({ id, body: data })
        } else {
            createAssesment(data)
        }
        setOpen(false)
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="course_id"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Course</FormLabel>
                            <FormControl>
                                <Select
                                    value={field.value && field.value !== 0 ? String(field.value) : undefined}
                                    onValueChange={(val) => field.onChange(Number(val))}
                               >
                                    <SelectTrigger className="w-full">
                                        <SelectValue placeholder="Select a course" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {courses?.items?.map((c) => (
                                            <SelectItem key={c.id ?? undefined} value={String(c.id ?? "")}>
                                                {c.code} — {c.name}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Name</FormLabel>
                            <FormControl>
                                <Input {...field} type="text" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />
                <FormField
                    control={form.control}
                    name="description"  
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Description</FormLabel>
                            <FormControl>
                                <Input {...field} type="text" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />   
                <FormField
                    control={form.control}
                    name="type"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Type</FormLabel>
                            <FormControl>
                                <Input {...field} type="text" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />
                <FormField
                    control={form.control}
                    name="start_date"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Start Date</FormLabel>
                            <FormControl>
                                <Input {...field} type="date" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />
                <FormField
                    control={form.control}
                    name="end_date"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>End Date</FormLabel>
                            <FormControl>
                                <Input {...field} type="date" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />
                <FormField
                    control={form.control}
                    name="weight"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Weight</FormLabel>
                            <FormControl>
                                <Input {...field} type="number" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />
                <FormField
                    control={form.control}
                    name="final_grade"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Final Grade</FormLabel>
                            <FormControl>
                                <Input {...field} type="number" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )} />
                <Button type="submit">{edit ? "Update" : "Create"}</Button>
            </form>
        </Form>
    )
}