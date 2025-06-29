function validateLoginForm() {
  const user = document.getElementById("userid")?.value.trim();
  const pass = document.getElementById("password")?.value;
  if (!user || !pass) {
    alert("User ID and Password are required.");
    return false;
  }
  return true;
}

function validateRegisterForm() {
  const name = document.getElementById("name")?.value.trim();
  const email = document.getElementById("email")?.value.trim();
  const password = document.getElementById("password")?.value;
  const confirm = document.getElementById("confirm")?.value;

  if (!name || !email || !password || !confirm) {
    alert("All fields are required.");
    return false;
  }

  if (!/^[^ ]+@[^ ]+\.[a-z]{2,3}$/.test(email)) {
    alert("Invalid email format.");
    return false;
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters.");
    return false;
  }

  if (password !== confirm) {
    alert("Passwords do not match.");
    return false;
  }

  return true;
}

function validateStudentForm() {
  const name = document.getElementById("studentName")?.value.trim();
  const email = document.getElementById("studentEmail")?.value.trim();
  const dob = document.getElementById("dob")?.value;
  const gender = document.getElementById("gender")?.value;
  if (!name || !email || !dob || !gender) {
    alert("All fields are required.");
    return false;
  }
  return true;
}

function validateSubjectForm() {
  const name = document.getElementById("subject")?.value.trim();
  const code = document.getElementById("code")?.value.trim();
  if (!name || !code) {
    alert("Subject Name and Code are required.");
    return false;
  }
  return true;
}

function validateUnitForm() {
  const title = document.getElementById("unitTitle")?.value.trim();
  const desc = document.getElementById("unitDesc")?.value.trim();
  if (!title || !desc) {
    alert("Unit Title and Description are required.");
    return false;
  }
  return true;
}

function validateProgramForm() {
  const name = document.getElementById("programName")?.value.trim();
  const code = document.getElementById("programCode")?.value.trim();
  if (!name || !code) {
    alert("Program Name and Code are required.");
    return false;
  }
  return true;
}

function validateCourseForm() {
  const name = document.getElementById("courseName")?.value.trim();
  if (!name) {
    alert("Course name is required.");
    return false;
  }
  return true;
}

function validateSemesterForm() {
  const course = document.getElementById("course")?.value;
  const sem = document.getElementById("semester")?.value;
  if (!course || !sem) {
    alert("Course and Semester must be selected.");
    return false;
  }
  return true;
}

function validateUploadForm() {
  const file = document.getElementById("file")?.value;
  if (!file) {
    alert("Please upload a syllabus file.");
    return false;
  }
  return true;
}

function validateSearchForm() {
  const keyword = document.getElementById("search")?.value.trim();
  if (!keyword) {
    alert("Please enter a search keyword.");
    return false;
  }
  return true;
}
