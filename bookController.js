exports.borrowBook = async (req, res) => {

    const bookId = req.params.id;

    const book = await Book.findById(bookId);

    if (!book) {
        return res.status(404).json({
            success: false,
            message: "Book not found"
        });
    }

    if (book.availableQuantity === 0) {
        return res.status(400).json({
            success: false,
            message: "Book is currently unavailable"
        });
    }

    const alreadyBorrowed =
        await Borrow.findOne({
            member: req.user.id,
            book: bookId,
            returned: false
        });

    if (alreadyBorrowed) {
        return res.status(400).json({
            success: false,
            message:
                "Book already borrowed"
        });
    }

    await Borrow.create({
        member: req.user.id,
        book: bookId
    });

    book.availableQuantity -= 1;

    await book.save();

    res.status(200).json({
        success: true,
        message: "Book borrowed successfully"
    });
};