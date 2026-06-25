router.post(
    "/",
    auth,
    role("librarian"),
    addBook
);

router.get(
    "/",
    auth,
    getBooks
);

router.get(
    "/:id",
    auth,
    getBook
);

router.put(
    "/:id",
    auth,
    role("librarian"),
    updateBook
);

router.delete(
    "/:id",
    auth,
    role("librarian"),
    deleteBook
);

router.post(
    "/:id/borrow",
    auth,
    role("member"),
    borrowBook
);

router.post(
    "/:id/return",
    auth,
    role("member"),
    returnBook
);