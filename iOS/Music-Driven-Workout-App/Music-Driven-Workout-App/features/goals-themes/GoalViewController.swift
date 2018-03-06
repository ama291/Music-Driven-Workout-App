//
//  GoalViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Jessica Wang on 3/5/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class GoalViewController: UIViewController {
    
    let request = APIRequest()
    
    @IBOutlet weak var goalNameLabel: UILabel!
    
    var selectedGoal: [String:Any]!
    var goal: String! = "goal"
    var userid: String!
    var reply: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(self.selectedGoal)
        if selectedGoal == nil {
            return
        }
        self.goal = String(describing: selectedGoal!["name"]!)
        self.goalNameLabel.text = self.goal
        // Do any additional setup after loading the view.
    }
    
    @IBAction func deleteGoal(_ sender: Any) {
        let qstr = "userid=\(userid!)&name=\(goal!)&key=SoftCon2018"
        self.request.submitPostLocal(route: "/api/goals/removegoal/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = self.request.parseJsonInitial(data: data!)
            if self.reply != "0" {
                print("Remove goal request failed")
                return
            }
        }.resume()
        self.performSegue(withIdentifier: "toGoalsList", sender: nil)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    
}
