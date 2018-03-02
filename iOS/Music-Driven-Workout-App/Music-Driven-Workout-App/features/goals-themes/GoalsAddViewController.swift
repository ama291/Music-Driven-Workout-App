//
//  GoalsAddViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class GoalsAddViewController: UIViewController {
    
    var userid: String!
    var name: String!
    var dsc: String!
    var goalnum: String!
    var categories: String!
    var musclegroups: String!
    var duration: String!
    var daysperweek: String!
    var notify: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("userid")
        print(userid)
        // Do any additional setup after loading the view.
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
    
    @objc func addGoalAPI() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/goals/addgoal/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        //userid, name, description, goalnum, categories, musclegroups, duration, dayssperweek, notify, key
        let postString = "userid=" + userid + "&name=" + name
        let postString2 = postString + "&description=" + dsc + "&goalnum=" + goalnum + "&categories=" + categories
        let postString3 = postString2 + "&musclegroups=" + musclegroups + "&duration=" + duration
        let postString4 = postString3 + "&daysperweek=" + daysperweek + "&notify=" + notify + "&key=SoftCon2018"
        request.httpBody = postString4.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                self.userid = json.Result
                print(self.userid)
            }

        }.resume()
    }
    
    @IBAction func goBackToGoalsMenu(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsID") as! GoalsMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goBackToGoalsHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsID") as! GoalsMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }

}
