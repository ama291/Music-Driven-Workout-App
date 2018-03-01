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
    var userid: String!  // this variable MUST be passed through all Scenes except Login
    
    /* * Navigation Samples * */
    /* For passing variables along a segue */
    func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is WorkSummaryViewController {
            let vc = segue.destination as? WorkSummaryViewController  // Declare our dest view controller
            vc?.userid = userid!    // Set dest vc var userid to be the userid held in this instance
        }
    }
    /* For navigating and passing variables to a VC on a separate storyboard */
    func goToHome() {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)  // Main = Main.storyboard
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController  // homeID = the StoryboardID for the target ViewController in the target storyboard
        vc.userid = userid!  // Setting target VC variables
        vc.present(vc, animated: true, completion: nil)  // remove the 'vc.' here when this is actually bound to a button
    }
}
