function helpRedirect() {
    let localPath = window.location.pathname + window.location.search;
    const linkDictionary = {
        "/dataingest/upload/": "/datasheet-documentation",
        "/crud/model-set/": "/datasheet-documentation#select4",

        "/crud": "/database-documentation",
        "/crud/students/": "/database-documentation#select1",
        "/crud/teachers/": "/database-documentation#select2",
        "/crud/schedules/": "/database-documentation#select3",
        "/crud/courses/": "/database-documentation#select4",
        "/crud/sections/": "/database-documentation#select5",
        "/crud/create-preference/": "/database-documentation#select6",
        "/crud/preferences/": "/database-documentation#select6",

        "/set-crud/courses/": "/databaseUp-documentation#select7",
        "/crud/create-bulk-sections/": "/databaseUp-documentation#select8",
        "/set-crud/preferences/": "/databaseUp-documentation#select9",

        "/set-crud/students/": "/studentData-documentation",

        "/check-schedule": "/schedule-documentation#select1",
        "/schedule": "/schedule-documentation#select2",
        "/": "/docs"
    }
    let newHref = linkDictionary[localPath];
    if (newHref === undefined) {
        newHref = "/docs";
    }
    window.location.href = "../../../../../../";
    window.location.href = newHref;
}