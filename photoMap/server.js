const express = require("express");
const fs = require("fs");

const app = express();

const data = JSON.parse(fs.readFileSync("./location_data.json"));
const key = fs.readFileSync("./key.txt", "utf8");

app.use("/", express.static("public"));

app.get("/data", (req, res) => {
	res.status(200).json(data);
});

app.get("/api-key", (req, res) => {
	res.status(200).json({ key });
});

app.listen(3000, () => {});
