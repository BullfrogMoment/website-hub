const otpSection = document.getElementById("main-otp-container");
const getOTPButton = document.getElementById("get-otp-button");

const countryCodeDropDown = document.getElementById("country-code");
const phoneNumTextBox = document.getElementById("phone-num-text-box");
let userContactInfo
let isEmail = true
let isPhoneNumber = true

const signInButton = document.getElementById("sign-in-button");

const firstDigitTextBox = document.getElementById("first-digit-text-box");
const secondDigitTextBox = document.getElementById("second-digit-text-box");
const thirdDigitTextBox = document.getElementById("third-digit-text-box");
const fourthDigitTextBox = document.getElementById("fourth-digit-text-box");

const incorrectOTP = document.getElementById("incorrect-otp");

let otpButtonClicked = 0; //0 for no, 1 for yes

//Hides attributes
getOTPButton.classList.add("is-hidden"); //Hidden
signInButton.classList.add("is-hidden"); //Hidden
otpSection.classList.add("is-hidden"); //Hidden
incorrectOTP.classList.add("is-hidden"); //Hidden

//Checks if the text box is full
phoneNumTextBox.addEventListener("input", function() {
  const value = phoneNumTextBox.value;
  if (isNaN(value)) {
    // It's a string (email)
    isPhoneNumber = false
    
    isEmail = true
    countryCodeDropDown.classList.add("drop-down-slide-out");

    phoneNumTextBox.minLength = 6;
    phoneNumTextBox.maxLength = 254;
  } else {
    // It's a number (phone)
    isEmail = false
    isPhoneNumber = true
    countryCodeDropDown.classList.remove("drop-down-slide-out");
    phoneNumTextBox.minLength = 10;
    phoneNumTextBox.maxLength = 10;
  }
  if (
    value.length >= phoneNumTextBox.minLength &&
    value.length <= phoneNumTextBox.maxLength &&
    otpButtonClicked === 0
  ) {
    getOTPButton.classList.remove("is-hidden");
  } else {
    getOTPButton.classList.add("is-hidden");
  }
});

//Takes user info and sends it to the server
getOTPButton.addEventListener("click", async function () {
  otpButtonClicked = 1;
  if (isEmail === true){
    userContactInfo = {
    "email": phoneNumTextBox.value,
    "phone_number": null
    }
  }else{
    userContactInfo = {
    "email": null,
    "phone_number": phoneNumTextBox.value
    }
  }
  

  getOTPButton.classList.add("is-hidden");
  otpSection.classList.remove("is-hidden");
  signInButton.classList.remove("is-hidden");


  // Sends the user's phone number/email
  const response = await fetch("/receive_details", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userContactInfo),
  });
});

signInButton.addEventListener("click", async function () {
  const userEnteredOTP = {
    identifier : phoneNumTextBox.value,
    first_digit: firstDigitTextBox.value,
    second_digit: secondDigitTextBox.value,
    third_digit: thirdDigitTextBox.value,
    fourth_digit: fourthDigitTextBox.value,
  };
  const sendOTP = await fetch("/verify_otp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userEnteredOTP),
  });
  pythonResponse = await sendOTP.json();
  console.log(pythonResponse.message);
  if (pythonResponse.message === "correct OTP") {
    window.location.href = "/home";
  }
  if (pythonResponse.message === "incorrect OTP") {
    firstDigitTextBox.value = "";
    secondDigitTextBox.value = "";
    thirdDigitTextBox.value = "";
    fourthDigitTextBox.value = "";
    incorrectOTP.classList.remove("is-hidden");
  }
});
