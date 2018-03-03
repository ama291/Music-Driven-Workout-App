//
//  ThemesAddViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ThemesAddViewController: UIViewController {
    
    var userid: String!
    
    let request = APIRequest()
    var themeName: String!
    var theme: String!
    var numWorkouts: Int! = 3
    
    @IBOutlet weak var numWorkoutsLabel: UILabel!
    @IBAction func numWorkoutsSlider(_ sender: Any) {
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.numWorkoutsLabel.text = "Number of Workouts: \(numWorkouts)"
        
//
//        self.frequencies = [[String:Any]]()
//        print(self.frequencies)
//        print(exChoices, userid, category, numEx)
//        var trackedStr: String = ""
//        trackedStr = exChoices.map { String($0) }.joined(separator: ",")
//        if trackedStr == "" {
//            trackedStr = "144"
//        }
//        let qstr = "categories=\(category)&numexercises=\(numEx)&exerciseids=\(trackedStr)&key=SoftCon2018"
//        self.request.submitPostServer(route: "/api/fitness/test/", qstring: qstr) { (data, response, error) -> Void in
//            if let error = error {
//                fatalError(error.localizedDescription)
//            }
//            self.reply = self.request.parseJsonRespone(data: data!)!
//            self.exercises = self.reply
//            self.exerciseInfo = self.exercises.removeFirst()
//
//            let vmitems = self.reply.map { ViewModelItem(item: Model(title: $0["name"] as! String, data: $0)) }
//            self.viewModel.setItems(items: vmitems)
//
//
//            DispatchQueue.main.async {
//                self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
//                self.tableView?.dataSource = self.viewModel
//                self.tableView?.delegate = self.viewModel
//                self.tableView?.estimatedRowHeight = 100
//                self.tableView?.rowHeight = UITableViewAutomaticDimension
//                self.tableView?.allowsSelection = false
//                self.tableView?.separatorStyle = .none
//            }
//
//            }.resume()
        

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func goBackToThemesMenu(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
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
