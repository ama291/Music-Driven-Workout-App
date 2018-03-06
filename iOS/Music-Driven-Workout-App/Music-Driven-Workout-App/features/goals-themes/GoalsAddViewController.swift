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
    
    let request = APIRequest()
    
    var userid: String! = "21"
    var goalName: String! = "goal1"
    var goalDescription: String! = "goaldescrip1"
    var goalNum: Int = 1
    var duration: Int = 1
    var daysperweek: Int = 1
    var reply: String?
    
    @IBOutlet weak var goalNameTextField: UITextField!
    @IBOutlet weak var goalDescriptionBox: UITextView!
    
    @IBOutlet weak var durationLabel: UILabel!
    @IBAction func durChanged(_ sender: UISlider){
        self.duration = Int(sender.value)
        durationLabel.text = "Duration: " + String(duration)
    }
    
    @IBOutlet weak var daysLabel: UILabel!
    @IBAction func daysChanged(_ sender: UISlider) {
        self.daysperweek = Int(sender.value)
        daysLabel.text = "Days per week: " + String(daysperweek)
    }
    
    @IBOutlet weak var numGoalsLabel: UILabel!
    @IBAction func numChanged(_ sender: UISlider) {
        self.goalNum = Int(sender.value)
        numGoalsLabel.text = "Number of Goals: " + String(goalNum)
    }
    
    @IBAction func saveGoal(_ sender: Any) {
        self.goalName = self.goalNameTextField.text
        self.goalDescription = self.goalDescriptionBox.text
        
        //userid, name, description, goalnum, categories, musclegroups, duration, dayssperweek, notify, key
        let qstr = "userid=\(userid!)&name=\(goalName!)&description=\(goalDescription!)&goalnum=\(goalNum)&categories=Cardio&musclegroups=Abs&duration=\(duration)&daysperweek=\(daysperweek)&notify=true&key=SoftCon2018"
        self.request.submitPostLocal(route: "/api/goals/addgoal/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = self.request.parseJsonInitial(data: data!)
            print (self.reply)
            if self.reply != "0" {
                print("Add goal request failed")
                return
            }
            }.resume()
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("userid: ", global.userid)
        self.numGoalsLabel.text = "Number of Goals: \(goalNum)"
        self.durationLabel.text = "Duration: \(goalNum)"
        self.numGoalsLabel.text = "Number of Goals: \(goalNum)"
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
