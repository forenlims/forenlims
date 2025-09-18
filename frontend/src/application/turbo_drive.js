
// This is the style entry file
import "../styles/turbo_drive.css";
import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";

const application = Application.start();

const context = require.context("../controllers", true, /\.js$/);
application.load(definitionsFromContext(context));

window.document.addEventListener("DOMContentLoaded", function () {
  window.console.log("dom ready");
});
