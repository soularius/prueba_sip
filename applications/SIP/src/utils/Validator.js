"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateStudent = void 0;
var validateStudent = function (student) {
    var errors = [];
    if (!student.name)
        errors.push("El nombre es obligatorio");
    return errors;
};
exports.validateStudent = validateStudent;
//# sourceMappingURL=Validator.js.map