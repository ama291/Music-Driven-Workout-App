//
//  GoalsAddViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class GoalsAddViewController: UIViewController {
    
    var audiostreaming: SPTAudioStreamingController!
    var player: SPTAudioStreamingController!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("userid: ", global.userid)
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* Navigation */
//    @IBAction func goToHome(_ sender: UIButton) {
//        let storyboard = UIStoryboard(name: "Main", bundle: nil)
//        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
//        vc.userid = userid!
//        present(vc, animated: true, completion: nil)
//    }
    
//        @IBAction func goBack(_ sender: UIButton) {
//            let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
//            let vc = storyboard.instantiateViewController(withIdentifier: "goalsID") as! GoalsMenuViewController
//            vc.userid = "1"
//            present(vc, animated: true, completion: nil)
//        }

//    @IBAction func back(_sender: UIButton) {
//        let myVC = storyboard?.instantiateViewController(withIdentifier: "goalsID") as! GoalsMenuViewController
//        myVC.userid = userid!
//        navigationController?.pushViewController(myVC, animated: true)
//    }
    
    @IBAction func goBackToGoalsMenu(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsID") as! GoalsMenuViewController
        present(vc, animated: true, completion: nil)
    }
}
