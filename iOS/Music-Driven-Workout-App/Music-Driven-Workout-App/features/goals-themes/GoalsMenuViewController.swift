//
//  GoalsMenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class GoalsMenuViewController: UIViewController, UITableViewDelegate, UITableViewDataSource{
    
//}, UITableViewController {

    var userid: String!
    var tableArray = [String:Any] ()
    
    var name: String!
    
    var passedUserId = String()
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.dataSource = self
        self.tableView.delegate = self
        // Do any additional setup after loading the view.
        populateGoals()
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
    
    struct goalsResult: Codable {
        var Result: String
        var Status: String
    }
    
    func populateGoals() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/goalssaved/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + userid + "&key=SoftCon2018"
        passedUserId = userid
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            guard let content = data else {
                print("not returning data")
                return
            }
//            guard let json = try? JSONDecoder().decode(goalsResult.self, from: data!) else { return }
            guard let json = (try? JSONSerialization.jsonObject(with: content, options: JSONSerialization.ReadingOptions.mutableContainers)) as? [String: Any] else {
                print("Not containing JSON")
                return
            }
//            let jsonRes = json["Result"]!
            if let array = json as? [String : Any] {
                self.tableArray = array
                print(self.tableArray)
            }
            print(self.tableArray)
            DispatchQueue.main.async {
                self.tableView.reloadData()
            }
            }.resume()
    }
    
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
 
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath) as UITableViewCell
        cell.textLabel?.text = (self.tableArray["Result"]! as! String)
        return cell
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.tableArray.count/2
    }
    
//    @IBAction func addGoal(_sender: UIButton) {
//        let myVC = storyboard?.instantiateViewController(withIdentifier: "goalsAdd") as! GoalsAddViewController
//        myVC.userid = passedUserId
//        navigationController?.pushViewController(myVC, animated: true)
//    }
    
    @IBAction func goToAddGoal(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsAdd") as! GoalsAddViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    
    func removeGoalAPI() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/goals/removegoal/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        //userid, name, key
        let postString = "userid=" + userid + "name=" + name + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                self.userid = json.Result
                print(self.userid)
            }
            }.resume()
    }
    
    @IBAction func removeTheme(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        vc.userid = userid!
        //removeThemeAPI()
        present(vc, animated: false, completion: nil)
    }
}
