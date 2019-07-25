//
//  LoginAndCheckWelcomeView.swift
//  LoginAndCheckWelcomeView
//
//  Created by Ehsan Zilaei on 2019-07-25.
//  Copyright © 2019 Facebook. All rights reserved.
//

import XCTest

class LoginAndCheckWelcomeView: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        // Put setup code here. This method is called before the invocation of each test method in the class.
        
        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false
        
        // UI tests must launch the application that they test. Doing this in setup will make sure it happens for each test method.
        app = XCUIApplication()
        app.launchArguments.append("--uiTestLoginAndWelcome")       // Shall check if application launched with arguments, otherwise app should be reset and relaunched.
        app.launch()
        
        // In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
    }

    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testExample() {
        // Use recording to get started writing UI tests.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        //app.otherElements["ChangeLogInUser"].tap()
        
        XCTAssertTrue(app.otherElements["ViewLogin"].exists)
        
        if (app.otherElements["ChangeLogInUser"].exists) {
            app.otherElements["Logga in som en annan användare"].tap()
        }
        
        XCUIApplication().textFields["ÅÅÅÅMMDDXXXX"].tap()
        
        // Log in with test user
        let test_user = ProcessInfo.processInfo.environment["TEST_USER_PNO"]!
        XCUIApplication()/*@START_MENU_TOKEN@*/.textFields["ÅÅÅÅMMDDXXXX"]/*[[".otherElements.matching(identifier: \"Mitt\\nHelsingborg Logga in med BankID Personnummer ÅÅÅÅMMDDXXXX Logga in Läs mer om hur du skaffar mobilt BankID\")",".otherElements[\"Logga in med BankID Personnummer ÅÅÅÅMMDDXXXX Logga in Läs mer om hur du skaffar mobilt BankID\"]",".otherElements[\"Personnummer ÅÅÅÅMMDDXXXX Logga in\"]",".otherElements[\"ÅÅÅÅMMDDXXXX\"].textFields[\"ÅÅÅÅMMDDXXXX\"]",".textFields[\"ÅÅÅÅMMDDXXXX\"]"],[[[-1,4],[-1,3],[-1,2,3],[-1,1,2],[-1,0,1]],[[-1,4],[-1,3],[-1,2,3],[-1,1,2]],[[-1,4],[-1,3],[-1,2,3]],[[-1,4],[-1,3]]],[0]]@END_MENU_TOKEN@*/.typeText(test_user)
        
        app/*@START_MENU_TOKEN@*/.otherElements["Logga in"]/*[[".otherElements.matching(identifier: \"Mitt\\nHelsingborg Logga in med BankID Personnummer Logga in Läs mer om hur du skaffar mobilt BankID\")",".otherElements[\"Logga in med BankID Personnummer Logga in Läs mer om hur du skaffar mobilt BankID\"]",".otherElements[\"Personnummer Logga in\"].otherElements[\"Logga in\"]",".otherElements[\"Logga in\"]"],[[[-1,3],[-1,2],[-1,1,2],[-1,0,1]],[[-1,3],[-1,2],[-1,1,2]],[[-1,3],[-1,2]]],[0]]@END_MENU_TOKEN@*/.tap()
        
        
        
        //let loginViewLoaded = (app.otherElements["ViewLoginSuccess"].exists)
        //XCTWaiter.wait(for: [loginViewLoaded], timeout: 60)
        
        // Wait a maximum of 60 secunds for user to login with BankID and
        // check in next view loaded.
        let exp = expectation(description: "Waiting for ViewLogin to load")
        let result = XCTWaiter.wait(for: [exp], timeout: 30)
        
        if result == XCTWaiter.Result.timedOut {
            XCTAssertTrue(app.otherElements["ViewGreetings"].exists)
        } else {
            XCTFail("Delay interrupted")
        }
    }
    
    // Set test states for persistant data (databases, user settings and so on).
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]?) -> Bool {
        if CommandLine.arguments.contains("--uiTestLoginAndWelcome") {
            // resetState()
            print("Resetting app for testing.")
        }
        
        return true
    }
}
