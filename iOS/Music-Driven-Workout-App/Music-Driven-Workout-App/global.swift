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
    var session: SPTSession!                // set in LoginVC (?)
    var token: String!                      // set in LoginVC & MenuViewVC
    
    /* * Global Methods * */
    func reset() {
        self.userid = nil
        self.username = nil
        self.session = nil
        self.token = nil
    }
    
    func printAll() {
        print("Global Variables:")
        print("\t userid: \(userid)")
        print("\t username: \(username)")
        print("\t auth: \(auth)")
        print("\t session: \(session)")
        print("\t token: \(token)")
    }
}
