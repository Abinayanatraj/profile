exports.returnBook = async (req, res) => {

    const borrow = await Borrow.findOne({
        member: req.user.id,
        book: req.params.id,
        returned: false
    });

    if (!borrow) {
        return res.status(400).json({
            success: false,
            message: "Book not borrowed"
        });
    }

    borrow.returned = true;

    await borrow.save();

    const book = await Book.findById(
        req.params.id
    );

    book.availableQuantity += 1;

    await book.save();

    res.status(200).json({
        success: true,
        message: "Book returned successfully"
    });
};