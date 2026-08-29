const express = require("express");
const cors = require("cors");
const multer = require("multer");

const app = express();

app.use(cors());
app.use(express.json());

const upload = multer({
    dest: "uploads/"
});

app.get("/", (req, res) => {
    res.json({
        message: "OCR backend is running"
    });
});

app.post("/ocr", upload.single("image"), (req, res) => {

    console.log("Received image:");
    console.log(req.file);

    res.json({
        message: "Image received",
        filename: req.file.filename
    });
});

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});