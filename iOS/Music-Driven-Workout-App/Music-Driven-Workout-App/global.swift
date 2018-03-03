//
//  global.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/27/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import Foundation

class Global {
    // !! There should only be one instantiation of this class in LoginViewController.swift !!
    
    
    /* * Persistent Global variables * */
    var userid: String!                     // set in LoginVC
    var username: String!                   // set in LoginVC
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var token:String!                       // set in LoginVC
    
    /* * Global Methods * */
    // For navigating and passing variables to a VC on a separate storyboard
    func goToHome() {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)  // Main = Main.storyboard
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController  // homeID = the StoryboardID for the target ViewController in the target storyboard
        vc.present(vc, animated: true, completion: nil)  // remove the 'vc.' here when this is actually bound to a button
    }
}
