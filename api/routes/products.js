const ctrlProduct = require("../controllers/products");
const ctrlUpdate = require("../controllers/update");
const upload = require("../middleware/updateFile");
const Router = require("express").Router;
const router = Router();

router.route("/").get(ctrlProduct.getAll);
router.get("/static", ctrlProduct.getStatic);
router.post("/update", upload.single("file"), ctrlUpdate.add);

module.exports = router;
