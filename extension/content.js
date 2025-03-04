// Add styles for the fill icon
const monthMapping = {
  jan: "01",
  feb: "02",
  mar: "03",
  apr: "04",
  may: "05",
  jun: "06",
  jul: "07",
  aug: "08",
  sep: "09",
  oct: "10",
  nov: "11",
  dec: "12",
};

const districtMapping = {
  Kathmandu: "1",
  Lalitpur: "2",
  Bhaktapur: "3",
  tanahun: "38",
  gulmi: "52",
  parsa: "22",
  ramechhap: "24",
  makawanpur: "32",
  sunsari: "14",
  rupandehi: "48",
};
const gendermapping = {
  male: "M",
  female: "F",
};

function getData() {
  return new Promise((resolve) => {
    chrome.storage.local.get("extractedData", (result) => {
      console.log("Retrieved Data:", result);
      resolve(result.extractedData.extracted_data || {}); // Ensure it's an object
    });
  });
}

async function main() {
  let dummyData = await getData();
}

main(); // Call the async function

const style = document.createElement("style");
style.textContent = `
  .form-fill-icon {
    cursor: pointer;
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #5f6368;
    background: transparent;
    border-radius: 50%;
    transition: background-color 0.2s;
    z-index: 2;
  }
  .form-fill-icon:hover {
    background-color: rgba(95, 99, 104, 0.1);
  }
  .form-fill-wrapper {
    position: relative;
    width: 100%;
  }
  .form-fill-tooltip {
    position: absolute;
    background: #333;
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 12px;
    bottom: calc(100% + 5px);
    right: 0;
    white-space: nowrap;
    display: none;
    z-index: 1000;
  }
  .form-fill-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    right: 10px;
    border: 5px solid transparent;
    border-top-color: #333;
  }
  .form-fill-icon:hover .form-fill-tooltip {
    display: block;
  }
`;
document.head.appendChild(style);

// Modified selectors to target Google's input fields
const selectors = {
  email: [
    'input[type="email"]',
    'input[autocomplete="username"]',
    'input[name="identifier"]',
    'input[id="identifierId"]',
    'input[type="text"][aria-label*="Email"]',
    'input[type="text"][aria-label*="Phone"]',
  ],
  full_name: [
    'input[name*="full_name" i]',
    'input[name*="fullname" i]',
    'input[id*="full_name" i]',
    'input[placeholder*="Full Name" i]',
    'input[aria-label*="Full Name" i]',
  ],
  first_name: [
    'input[name*="first_name" i]',
    'input[name*="firstname" i]',
    'input[id*="first_name" i]',
    'input[placeholder*="First Name" i]',
    'input[aria-label*="First Name" i]',
  ],
  last_name: [
    'input[name*="last_name" i]',
    'input[name*="lastname" i]',
    'input[id*="last_name" i]',
    'input[placeholder*="Last Name" i]',
    'input[aria-label*="Last Name" i]',
  ],
  Birth_year: [
    'input[name*="year" i]',
    'input[id*="year" i]',
    'input[name*="birth_year" i]',
    'input[id*="birth_year" i]',
    'input[aria-label*="Year" i]',
    'select[name*="year" i]',
    'select[id*="year" i]',
  ],
  Birth_district: [
    'select[id*="birthDistrictPlace" i]',
    'input[id*="permanentDistrictPlace" i]',
    'select[id*="ccIssuingDistrict" i]',
  ],
  gender: ['select[id*="gender" i]'],
  citizenship_num: ['input[id*="ccNumberLoc" i]'],
  Birth_month: [
    'input[name*="month" i]',
    'input[name*="dob_loc" i]',
    'input[name*="birth_month" i]',
    'input[id*="dob" i]',
    'input[aria-label*="Month" i]',
    'select[name*="month" i]',
    'select[id*="dob" i]',
    'input[id*="date_of_birth_reg" i]',
    "",
  ],
  Birth_day: [
    'input[name*="day" i]',
    'input[id*="day" i]',
    'input[name*="birth_day" i]',
    'input[id*="birth_day" i]',
    'input[aria-label*="Day" i]',
    'select[name*="day" i]',
    'select[id*="day" i]',
  ],
  phone: [
    'input[type="tel"]',
    'input[name*="phone" i]',
    'input[name*="mobile" i]',
  ],
  address: ['input[name*="address" i]', 'input[name*="street" i]'],
  city: ['input[name*="city" i]'],
  state: ['input[name*="state" i]', 'select[name*="state" i]'],
  zipCode: ['input[name*="zip" i]', 'input[name*="postal" i]'],
  company: ['input[name*="company" i]', 'input[name*="organization" i]'],
  website: ['input[name*="website" i]', 'input[name*="url" i]'],
};

function getReadableFieldName(fieldType) {
  const fieldNames = {
    full_name: "Full Name",
    email: "Email",
    first_name: "first_name",
    lastName: "Last Name",
    phone: "Phone Number",
    address: "Address",
    city: "City",
    state: "State",
    zipCode: "ZIP Code",
    company: "Company",
    website: "Website",
  };
  return fieldNames[fieldType] || fieldType;
}

// Function to add icons to fields
async function addIconsToFields() {
  let dummyData = await getData(); // Ensure data is fetched before processing fields
  console.log("Searching for input fields...");

  for (const [field, fieldSelectors] of Object.entries(selectors)) {
    for (const selector of fieldSelectors) {
      const elements = document.querySelectorAll(selector);
      console.log(
        `Found ${elements.length} elements for selector: ${selector}`
      );

      elements.forEach((element) => {
        if (
          element.type === "hidden" ||
          element.style.display === "none" ||
          element.style.visibility === "hidden" ||
          element.hidden ||
          !element.offsetParent
        ) {
          console.log("Skipping hidden element");
          return;
        }

        console.log("Processing element:", element);

        if (element.parentElement.classList.contains("form-fill-wrapper")) {
          console.log("Element already wrapped, skipping");
          return;
        }

        // Create wrapper
        const wrapper = document.createElement("div");
        wrapper.classList.add("form-fill-wrapper");
        element.parentNode.insertBefore(wrapper, element);
        wrapper.appendChild(element);

        // Create fill icon
        const fillIcon = document.createElement("div");
        fillIcon.classList.add("form-fill-icon");
        fillIcon.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L14.85 8.35L22 9.24L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.24L9.15 8.35L12 2Z"></path>
          </svg>
          <div class="form-fill-tooltip">
            Fill ${getReadableFieldName(field)}: ${dummyData[field] || ""}
          </div>
        `;

        // Position the icon container relative to the input's padding
        const computedStyle = window.getComputedStyle(element);
        const paddingRight = parseInt(computedStyle.paddingRight) || 0;
        fillIcon.style.right = `${paddingRight + 8}px`;

        wrapper.appendChild(fillIcon);

        // Add click handler to the icon
        fillIcon.addEventListener("click", (e) => {
          e.stopPropagation();
          // element.value = dummyData["first_name"];

          if (dummyData[field] || field == "full_name") {
            if (field == "Birth_month") {
              element.value = `${dummyData["Birth_year"]}-${
                monthMapping[dummyData["Birth_month"]]
              }-${dummyData["Birth_day"]}`;
            } else if (field == "Birth_district") {
              element.value = districtMapping[dummyData["Birth_district"]];
            } else if (field == "gender") {
              element.value = gendermapping[dummyData[field]];
            } else if (field == "full_name") {
              element.value = `${dummyData["first_name"]} ${dummyData["last_name"]}`;
            } else {
              element.value = dummyData[field];
            }
            element.dispatchEvent(new Event("change", { bubbles: true }));
            element.dispatchEvent(new Event("input", { bubbles: true }));
          }
        });

        console.log("Successfully added icon to field");
      });
    }
  }
}

// Run when the document loads
document.addEventListener("DOMContentLoaded", addIconsToFields);

// Also run when content changes (for dynamically loaded forms)
const observer = new MutationObserver(addIconsToFields);
observer.observe(document.body, {
  childList: true,
  subtree: true,
});

// Update icons if storage changes
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Hello");
  if (message.action === "updatePage") {
    // Perform the necessary updates on the webpage
    addIconsToFields(); // Example function that interacts with the webpage
    console.log("Page updated");
    main(); // Example of another function that needs to run
  }
});

// Keep the original fillForms event listener
document.addEventListener("fillFormsButton", addIconsToFields);
